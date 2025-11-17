import { MigrationInterface, QueryRunner } from 'typeorm'

export class CreateNotesTable1770000000000 implements MigrationInterface {
  name = 'CreateNotesTable1770000000000'

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`CREATE TABLE "notes" (
      "id" TEXT PRIMARY KEY,
      "title" TEXT NOT NULL,
      "body" TEXT NOT NULL,
      "tags" TEXT NOT NULL DEFAULT '[]',
      "deleted_at" DATETIME,
      "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      "updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )`)

    // Indexes for optimization
    await queryRunner.query(`CREATE INDEX "IDX_notes_deleted_at" ON "notes" ("deleted_at")`)
    await queryRunner.query(`CREATE INDEX "IDX_notes_title" ON "notes" ("title")`)
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    // Drop indexes
    await queryRunner.query(`DROP INDEX IF EXISTS "IDX_notes_title"`)
    await queryRunner.query(`DROP INDEX IF EXISTS "IDX_notes_deleted_at"`)

    // Drop table
    await queryRunner.query(`DROP TABLE IF EXISTS "notes"`)
  }
}

