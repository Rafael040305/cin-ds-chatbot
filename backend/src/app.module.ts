import { Module } from '@nestjs/common';
import { AppController } from './app.controller.js';
import { AppService } from './app.service.js';
import { AiServiceModule } from './ai-service/ai-service.module.js';

@Module({
  imports: [AiServiceModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
