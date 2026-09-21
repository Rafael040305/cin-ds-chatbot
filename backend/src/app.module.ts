import { Module } from '@nestjs/common';
import { AppController } from './app.controller.js';
import { AppService } from './app.service.js';
import { AiServiceModule } from './ai-service/ai-service.module.js';
import { OrchestrationModule } from './orchestration/orchestration.module.js';

@Module({
  imports: [AiServiceModule, OrchestrationModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
