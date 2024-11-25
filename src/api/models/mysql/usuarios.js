/*
export class UsuariosModel {
  static async getAll(req, res) {
    return "El servidor esta funcionando correctamente";
  }

  static async getById(req, res) {

  }

  static async create(req, res) {
    const { nombres, apellidos, tipoDocumento, numeroDoc, municipio, departamento } = req.body;
    console.log(`
          Se ha creado un nuevo usuario con los datos:
          ${nombres} ${apellidos},
          ${tipoDocumento}: ${numeroDoc},
          ${municipio}, ${departamento}
        `);
  }

  static async delete(req, res) {

  }

  static async update(req, res) {

  }
}
*/
class User {
  constructor ({ Modelo }) {
    this.Modelo = Modelo
  }
}
export default User
