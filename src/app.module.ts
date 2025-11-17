import { Module } from '@nestjs/common'
import { TypeOrmModule } from '@nestjs/typeorm'
import { ConfigModule } from '@nestjs/config'
import { DataSource } from 'typeorm'
import { NotesModule } from './notes/notes.module'

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    TypeOrmModule.forRoot({
      type: 'better-sqlite3',
      database: ':memory:',
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      migrations: [__dirname + '/database/migrations/*{.ts,.js}'],
      // For in-memory DB, use synchronize in development (data doesn't persist anyway)
      // In production, migrations should be used
      synchronize: process.env.NODE_ENV !== 'production',
      migrationsRun: false, // Will run manually in main.ts if synchronize is false
    }),
    NotesModule,
  ],
})
export class AppModule {
  constructor(private dataSource: DataSource) {}
}

