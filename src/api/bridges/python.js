import { spawn } from 'child_process'
import { resolve } from 'path'
// import './gtp.js'
class ExecutePhython {
  #path
  #EntornoVirtual
  constructor ({ path, EntornoVirtual = null }) {
    this.#path = resolve(path)
    this.#EntornoVirtual = EntornoVirtual !== null
      ? resolve(EntornoVirtual, 'Scripts', 'activate.bat')
      : null
  }

  #CreateChildProcess () {
    const childProcess = spawn('cmd.exe', { shell: true })
    if (this.#EntornoVirtual) {
      childProcess.stdin.write(`"${this.#EntornoVirtual}"\n`)
    }
    childProcess.stdin.write(`python "${this.#path}"\n`)

    return childProcess
  }

  async executePhython (...params) {
    const parametros = params.join('\n')
    let response = ''
    const childProcess = this.#CreateChildProcess()

    childProcess.stdout.on('data', (data) => {
      response += data.toString()
      console.log(data.toString())
    })
    if (parametros) {
      childProcess.stdin.write(params.join('\n'))
    }
    childProcess.stdin.end()
    return new Promise((resolve, reject) => {
      childProcess.on('close', (code) => {
        if (code === 0) {
          resolve(response)
        } else {
          console.log(response)
          reject(new Error('Ocurrio un error inseperado '))
        }
      })
    })
  }
}
export default ExecutePhython
const e = new ExecutePhython({ path: '../scraping/policia.py', EntornoVirtual: '../../venv' })
e.executePhython()
/**
 * const proceso = spawn(comando, argumentos, { shell: true });
 */
/*
async function a () {
  const comando1 = 'cd'
  const ruta1 = '../../venv/Scripts/activate.bat'
  const cmd = spawn(comando1, [ruta1], { shell: true })

  let response = ''

  cmd.stdout.on('data', (data) => {
    response += data.toString()
    console.log('hola')
  })

  cmd.on('close', (code) => {
    console.log(response)
  })
  cmd.stdin.write('./activate\ncd ../../backend/scraping/\npython ./policia.py')
  cmd.stdin.end()
  /* const ref = new ExecutePhython({ path: '../scraping/policia.py', EntornoVirtual: '../../venv' })
  const response = await ref.executePhython()
  console.log(response)
}
a() */
