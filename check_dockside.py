import sys
import dockside

if "--strict" in sys.argv:
    sys.argv.remove("--strict")
    tester = dockside.teststrict
elif "--nowarn" in sys.argv:
    sys.argv.remove("--strict")
    tester = dockside.test_nowarnings
else:
    tester = dockside.test

sys.exit(tester(*sys.argv[1:]))
