import { OnWorkerEvent, Processor, WorkerHost } from "@nestjs/bullmq";
import { Job, Worker } from "bullmq";
import { NoteEntity } from "../note.entity";

@Processor("notifications")
export class NotificationsProcessor extends WorkerHost<Worker<NoteEntity, any, string>> {
  async process(job: Job<NoteEntity, any, string>) {
    // TODO: send email using note context
    console.log(
      `Dispatching notification for note "${job.data.title}" with body: ${job.data.body}`
    );
  }

  @OnWorkerEvent("active")
  onActive(job: Job<NoteEntity, any, string>) {
    console.log(
      `Processing job ${job.id} of type ${job.name} with data ${JSON.stringify(
        job.data
      )}...`
    );
  }
}
