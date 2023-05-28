node {
  withDockerContainer(image: "python:2-alpine:latest") {
    stage("Build") {
      sh 'python -m py_compile sources/add2vals.py sources/calc.py'
    }
  }
  withDockerContainer(image: "qnib/pytest:latest") {
    stage("Test") {
      sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
  }
 }
}
