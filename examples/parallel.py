from jisoo.models.state import Parallel, Pass, Chain, Succeed, Graph

c1 = Chain(steps=[Pass(id="Pass_1"), Succeed(id="Pass_2")])
c2 = Chain(steps=[Pass(id="Pass_3"), Pass(id="Pass_4")])

pl = Parallel(id="Parallel", branches=[c1, c2])

g = Graph(branch=Chain(steps=[pl]), comment="Parallel State", timeout_seconds=60)

print(g.definition)

g2 = Graph(branch=pl, comment="Parallel State", timeout_seconds=60)

print(g2.definition)
