import { RegisterQueueOptions } from "@nestjs/bullmq";

export const NOTIFICATIONS_QUEUE_OPTIONS: RegisterQueueOptions = {
  name: "notifications",
  defaultJobOptions: { removeOnFail: false },
};
