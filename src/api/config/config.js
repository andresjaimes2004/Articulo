const ENV = process.env
export const PORT = ENV.PORT ?? 3000
export const DATABASE_URL = ENV.DATABASE_URL ?? './db/example.sqlite'
export const ENVIRONMENT_PATH_PYTHON = ENV.ENVIRONMENT_PATH_PYTHON ?? '.'
export const SCRAPING_PATH_PYTHON = ENV.SCRAPING_PATH_PYTHON ?? '.'
const config = {
  PORT,
  DATABASE_URL,
  ENVIRONMENT_PATH_PYTHON,
  SCRAPING_PATH_PYTHON
}
export default config
