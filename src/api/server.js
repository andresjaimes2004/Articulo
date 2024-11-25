import express from 'express'
import { corsMiddleware } from './middlewares/cors.js'
import { PORT } from './config/config.js'
import usuariosRouter from './routes/usuarios.js'

const CreateApp = ({ Modelo }) => {
  const app = express()
  app.use(express.json())
  app.use(corsMiddleware())
  app.disable('x-powered-by')

  app.use('/usuarios', usuariosRouter)

  app.listen(PORT, () => {
    console.log(`Server listening on port http://localhost:${PORT}`)
  })
}

export default CreateApp
