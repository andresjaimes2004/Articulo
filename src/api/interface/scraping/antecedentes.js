import ExecutePhython from '../../bridges/python.js'
import { SCRAPING_PATH_PYTHON, ENVIRONMENT_PATH_PYTHON } from '../../config/config.js'

const rutaScrapingPolicia = `${SCRAPING_PATH_PYTHON}/policia.py`

const scrapingSisben = new ExecutePhython({ path: rutaScrapingPolicia, EntornoVirtual: ENVIRONMENT_PATH_PYTHON })

const SearchCriminalRecord = async ({ NumeroDeIdentificacion }) => {
  if (typeof NumeroDeIdentificacion !== 'number') throw new Error('El Numero de identificacion debe ser de tipo numerico')
  const datos = `${NumeroDeIdentificacion}`
  return await scrapingSisben.executePhython(datos)
}
/**
 * Ejemplo de uso
 * SearchDataUserForRegister({ NumeroDeIdentificacion: 1516516516 })
*/
export default SearchCriminalRecord
