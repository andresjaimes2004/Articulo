class E extends Error {
  constructor ({ message, name }) {
    super(message)
    this.name = name
  }
}
const e = new E({ message: 'el campo es requerido', name: 'cliente' })
console.log(e)
export default E
