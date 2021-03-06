import subprocess
from junit_xml import TestSuite, TestCase

def main():
    propFile= open( r"URL.properties", "rU" )
    propDict= dict()
    for propLine in propFile:
        propDef= propLine.strip()
        if len(propDef) == 0:
            continue
        if propDef[0] in ( '!', '#' ):
            continue
        punctuation= [ propDef.find(c) for c in ':= ' ] + [ len(propDef) ]
        found= min( [ pos for pos in punctuation if pos != -1 ] )
        name= propDef[:found].rstrip()
        value= propDef[found:].lstrip(":= ").rstrip()
        propDict[name]= value
    propFile.close()
    print(propDict)
    output= dict()
    for key, value in propDict.items():
        cmd="curl -Is "+value+"| head -n 1"
        print(cmd)
        process=subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = process.communicate()[0]
        if stdout.decode('utf-8').rstrip()=='':
            output[key]="Unable to Connect"
        else:
            output[key]=stdout.decode("utf-8").rstrip()

    print(output)

    test_cases=[]
    for i, (key, value) in enumerate(output.items()):
        testname="Test" + str(i)
        if value != "HTTP/1.1 200":
            test_cases.append(TestCase(testname, str(key), 1, str(value), 'failure'))
            test_cases[i].add_failure_info('Unable to Connect')
        else:
            test_cases.append(TestCase(testname, str(key), 1, str(value),''))

    ts = TestSuite("my test suite", test_cases)
    print(TestSuite.to_xml_string([ts]))
    with open('output.xml', 'w') as f:
        TestSuite.to_file(f, [ts], prettyprint=True)
"""
test_cases = [TestCase('Test1', 'some.class.name', 123.345, 'I am stdout!', 'I am stderr!')]
ts = TestSuite("my test suite", test_cases)
# pretty printing is on by default but can be disabled using prettyprint=False
print(TestSuite.to_xml_string([ts]))
"""
if __name__ == "__main__":
    main()
