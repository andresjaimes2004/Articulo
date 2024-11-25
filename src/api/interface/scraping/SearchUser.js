import ExecutePhython from '../../bridges/python.js'
import { SCRAPING_PATH_PYTHON, ENVIRONMENT_PATH_PYTHON } from '../../config/config.js'
import { validarNumeroDocumento } from '../../schema/validaciones.js'
const rutaScrapingSisben = `${SCRAPING_PATH_PYTHON}/sisben.py`

const scrapingSisben = new ExecutePhython({ path: rutaScrapingSisben, EntornoVirtual: ENVIRONMENT_PATH_PYTHON })

const SearchDataUserForRegister = async ({ NumeroDeIdentificacion }) => {
  const value = await validarNumeroDocumento(NumeroDeIdentificacion)
  const datos = `${value}}`
  return await scrapingSisben.executePhython(datos)
}
/**
 * Ejemplo de uso
 * SearchDataUserForRegister({ NumeroDeIdentificacion: 1516516516})
*/
export default SearchDataUserForRegister
