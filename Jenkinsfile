node {
  withDockerContainer(image: "python:2-alpine") {
    stage("Build") {
      sh 'python -m py_compile ./sources/add2vals.py ./sources/calc.py'
    }
  }
}
