import { NestFactory } from '@nestjs/core'
import { ValidationPipe } from '@nestjs/common'
import { AppModule } from './app.module'
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger'
import { DataSource } from 'typeorm'
import dotenv from 'dotenv'

dotenv.config()

async function bootstrap() {
  const app = await NestFactory.create(AppModule)

  // Execute migrations for in-memory database (only if synchronize is false)
  if (process.env.NODE_ENV === 'production') {
    const dataSource = app.get(DataSource)
    try {
      await dataSource.runMigrations()
      console.log('✅ Migrations executed successfully')
    } catch (error) {
      console.error('❌ Migration execution error:', error.message)
      throw error
    }
  } else {
    console.log('✅ Using synchronize mode for in-memory database (development)')
  }

  // Enable CORS
  app.enableCors()

  // Global validation pipe
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  )

  // Health endpoint
  app.getHttpAdapter().get('/health', (req, res) => {
    res.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      service: 'Notes Service API',
      version: '1.0.0',
    })
  })

  // Swagger configuration
  const config = new DocumentBuilder()
    .setTitle('Notes Service API')
    .setDescription('REST API for text notes management - Juspay Brazil Assignment')
    .setVersion('1.0.0')
    .addTag('Notes', 'Endpoints for notes management')
    .addServer(process.env.SERVER_URL || 'http://localhost:3000', 'Main Server')
    .build()

  const document = SwaggerModule.createDocument(app, config)
  SwaggerModule.setup('docs', app, document, {
    swaggerOptions: {
      persistAuthorization: true,
      tagsSorter: 'alpha',
      operationsSorter: 'alpha',
    },
    customSiteTitle: 'Notes Service API - Documentation',
    customCss: '.swagger-ui .topbar { display: none }',
  })

  const port = +process.env.SERVER_PORT || 3000
  await app.listen(port, '0.0.0.0')
  console.log(`🚀 Application is running on: http://localhost:${port}`)
  console.log(`📚 Swagger documentation: http://localhost:${port}/docs`)
}

bootstrap()

