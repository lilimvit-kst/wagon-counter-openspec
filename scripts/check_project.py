#!/usr/bin/env python3
"""Validate planning integrity and evidence structure; not runtime correctness."""
from pathlib import Path
import argparse,hashlib,json,re,sys

class ProjectError(Exception):
    pass

def require(condition,message):
    if not condition:
        raise ProjectError(message)

def local_file(root,name):
    p=(root/name).resolve()
    require(p.is_relative_to(root.resolve()) and p.is_file(),f'Нет допустимого файла: {name}')
    return p

def change_path(root,name):
    active=root/'openspec/changes'/name
    found=([active] if active.is_dir() else [])+list((root/'openspec/changes/archive').glob('????-??-??-'+name))
    require(len(found)==1,f'{name}: нужен один активный или архивный каталог')
    return found[0]

def inspect(root):
    root=root.resolve()
    for name in ['AGENTS.md','openspec/config.yaml','docs/OPENSPEC_RULES.md','package.json','package-lock.json']:
        local_file(root,name)
    d=json.loads(local_file(root,'docs/blocks.json').read_text())
    require(d['schema_version']==1 and d['sequence_policy']=='strict-b00-b14','Неизвестная схема/политика блоков')
    require(hashlib.sha256(local_file(root,d['source_file']).read_bytes()).hexdigest()==d['source_sha256'],'Исходное ТЗ изменилось; оформить редакцию и карту')
    blocks=d['blocks'];ids=[b['id'] for b in blocks]
    require(ids==[f'B{i:02}' for i in range(15)],'Нужны B00–B14 в правильном порядке')
    require(len({b['change'] for b in blocks})==15,'Повтор change')
    require(len({b['capability'] for b in blocks})==15,'Повтор новой capability')
    require(sum(b['status']=='in_progress' for b in blocks)<=1,'Одновременно один блок in_progress')
    all_r=set();all_s=set()
    for i,b in enumerate(blocks):
        bid=b['id'];status=b['status']
        require(status in {'planned','blocked','in_progress','verified'},f'{bid}: неверный статус')
        require(all(dep in ids[:i] for dep in b['dependencies']),f'{bid}: недопустимая/циклическая зависимость')
        p=change_path(root,b['change']);archived=p.parent.name=='archive'
        for name in ['proposal.md','design.md','tasks.md','.openspec.yaml']:
            require((p/name).is_file(),f'{bid}: нет {name}')
        text=local_file(root,str((p/'specs'/b['capability']/'spec.md').relative_to(root))).read_text()
        rs=re.findall(r'^### Requirement: (WC-B\d{2}-R\d{2})\b',text,re.M)
        ss=re.findall(r'^#### Scenario: (WC-B\d{2}-R\d{2}-S\d{2})\b',text,re.M)
        require(rs==b['requirements'] and ss==b['scenarios'],f'{bid}: карта Requirement/Scenario расходится со spec')
        require(len(set(rs))==len(rs) and not all_r.intersection(rs),f'{bid}: повтор Requirement')
        require(len(set(ss))==len(ss) and not all_s.intersection(ss),f'{bid}: повтор Scenario')
        all_r.update(rs);all_s.update(ss);local_file(root,b['report'])
        boxes=re.findall(r'^- \[([ xX])\] \d+\.\d+ ',(p/'tasks.md').read_text(),re.M)
        require(bool(boxes),f'{bid}: отсутствуют задачи')
        require(not archived or status=='verified',f'{bid}: непроверенный change в архиве')
        if status in {'in_progress','verified'}:
            require(all(x['status']=='verified' for x in blocks[:i]),f'{bid}: сначала завершить предыдущие блоки')
        if status=='verified':
            require(' ' not in boxes,f'{bid}: незавершенные задачи')
            v=b.get('verification');require(isinstance(v,dict),f'{bid}: требуется verification')
            require(bool(re.fullmatch('[0-9a-f]{40}',v.get('code_commit',''))),f'{bid}: полный hash проверенного кода')
            require(bool(v.get('accepted_mode')) and isinstance(v.get('limitations'),list),f'{bid}: режим и ограничения')
            require(isinstance(v.get('commands'),list) and bool(v['commands']),f'{bid}: нужны команды проверки')
            for c in v['commands']:
                require(bool(c.get('command')) and c.get('exit_code')==0,f'{bid}: команда не прошла')
                local_file(root,c['evidence_file'])
            require(set(v.get('scenarios',{}))==set(ss),f'{bid}: нет результатов всех Scenario')
            for sid,result in v['scenarios'].items():
                require(result.get('kind') in {'automated','manual'} and result.get('result')=='pass',f'{sid}: нет выполненной проверки')
                local_file(root,result['evidence_file'])
            if archived:
                local_file(root,'openspec/specs/'+b['capability']+'/spec.md')
    return d,len(all_r),len(all_s)

def can_start(root,d,bid):
    blocks=d['blocks'];ids=[b['id'] for b in blocks]
    require(bid in ids,f'Неизвестный блок {bid}');i=ids.index(bid)
    require(blocks[i]['status']!='verified',f'{bid}: уже завершен; доработка отдельным change')
    pending=[]
    for b in blocks[:i]:
        if b['status']!='verified':pending.append(b['id'])
        elif change_path(root,b['change']).parent.name!='archive':pending.append(b['id']+' (архивирование)')
    pending += [b['id'] for b in blocks if b['status']=='in_progress' and b['id']!=bid]
    require(not pending,f'{bid}: сначала завершить '+', '.join(pending))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--can-start');parser.add_argument('--status',action='store_true')
    a=parser.parse_args()
    try:
        d,nr,ns=inspect(a.root)
        if a.can_start:
            can_start(a.root,d,a.can_start);print(a.can_start+': можно начинать/продолжать порученную реализацию')
        elif a.status:
            for b in d['blocks']:print(b['id'],b['status'],b['change'])
        else:print(f'OK: 15 блоков; {nr} требований; {ns} сценариев; источник/карта согласованы')
        return 0
    except (ProjectError,KeyError,TypeError,ValueError,OSError) as e:
        print('ERROR: '+str(e),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
