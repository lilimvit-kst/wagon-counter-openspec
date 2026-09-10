import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
S=importlib.util.spec_from_file_location('gate',ROOT/'scripts/check_project.py');G=importlib.util.module_from_spec(S);S.loader.exec_module(G)
class GateTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)/'repo';self.root.mkdir()
        for folder in ['docs','openspec']:shutil.copytree(ROOT/folder,self.root/folder)
        for file in ['AGENTS.md','package.json','package-lock.json']:shutil.copyfile(ROOT/file,self.root/file)
        p=self.root/'docs/blocks.json';d=json.loads(p.read_text())
        for b in d['blocks']:
            old=G.change_path(self.root,b['change']);target=self.root/'openspec/changes'/b['change']
            if old!=target:shutil.move(str(old),str(target))
            t=target/'tasks.md';t.write_text(t.read_text().replace('- [x]','- [ ]').replace('- [X]','- [ ]'))
            b.update(status='planned',verification=None)
        p.write_text(json.dumps(d))
    def mutate(self,fn):
        p=self.root/'docs/blocks.json';d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d))
    def test_b00_allowed_b01_blocked(self):
        d,_,_=G.inspect(self.root);G.can_start(self.root,d,'B00')
        with self.assertRaisesRegex(G.ProjectError,'B00'):G.can_start(self.root,d,'B01')
    def test_source_drift(self):
        d=json.loads((self.root/'docs/blocks.json').read_text());p=self.root/d['source_file'];p.write_text(p.read_text()+'changed')
        with self.assertRaisesRegex(G.ProjectError,'ТЗ изменилось'):G.inspect(self.root)
    def test_verified_without_evidence(self):
        self.mutate(lambda d:d['blocks'][0].update(status='verified'))
        t=self.root/'openspec/changes/b00-contracts-foundation/tasks.md';t.write_text(t.read_text().replace('- [ ]','- [x]'))
        with self.assertRaisesRegex(G.ProjectError,'verification'):G.inspect(self.root)
    def test_cycle(self):
        self.mutate(lambda d:d['blocks'][0].update(dependencies=['B14']))
        with self.assertRaisesRegex(G.ProjectError,'зависимость'):G.inspect(self.root)
    def test_scenario_drift(self):
        p=self.root/'openspec/changes/b00-contracts-foundation/specs/contracts-foundation/spec.md';p.write_text(p.read_text().replace('WC-B00-R01-S01','WC-B00-R01-S99'))
        with self.assertRaisesRegex(G.ProjectError,'Scenario'):G.inspect(self.root)
if __name__=='__main__':unittest.main()
