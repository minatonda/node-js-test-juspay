import { DataSource } from 'typeorm'
import { NoteEntity } from '../../notes/note.entity'

export default new DataSource({
  type: 'better-sqlite3',
  database: ':memory:',
  entities: [NoteEntity],
  migrations: ['src/database/migrations/*.ts'],
  synchronize: false, // Disable auto-sync - use migrations
})

