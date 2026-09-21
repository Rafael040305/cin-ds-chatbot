import { createServer, type Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import { Test, type TestingModule } from '@nestjs/testing';
import { AppModule } from '../src/app.module.js';
import { AiService } from '../src/ai-service/ai-service.service.js';

describe('AiService (HTTP integration)', () => {
  let upstream: Server;
  let module: TestingModule;
  let received: { method?: string; url?: string; body: unknown };

  beforeEach(async () => {
    upstream = createServer((req, res) => {
      let body = '';
      req.setEncoding('utf8');
      req.on('data', (chunk: string) => {
        body += chunk;
      });
      req.on('end', () => {
        received = {
          method: req.method,
          url: req.url,
          body: JSON.parse(body) as unknown,
        };
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(
          JSON.stringify({ contexto: '', fontes: [], distancia_minima: 1 }),
        );
      });
    });
    await new Promise<void>((resolve, reject) => {
      upstream.once('error', reject);
      upstream.listen(0, '127.0.0.1', resolve);
    });
    const port = (upstream.address() as AddressInfo).port;
    vi.stubEnv('AI_SERVICE_URL', `http://127.0.0.1:${port}`);
    module = await Test.createTestingModule({ imports: [AppModule] }).compile();
  });

  afterEach(async () => {
    vi.unstubAllEnvs();
    await module?.close();
    if (upstream?.listening) {
      await new Promise<void>((resolve, reject) => {
        upstream.close((error) => (error ? reject(error) : resolve()));
        upstream.closeAllConnections();
      });
    }
  });

  it('resolve o serviço no NestJS e consulta um servidor HTTP', async () => {
    const consulta = {
      pergunta: 'Dispensa?',
      curso: 'CC',
      perfil: '2023',
      top_k: 2,
    };
    await expect(
      module.get(AiService).buscarContexto(consulta),
    ).resolves.toEqual({ contexto: '', fontes: [], distancia_minima: 1 });
    expect(received).toEqual({
      method: 'POST',
      url: '/api/v1/buscar',
      body: consulta,
    });
  });
});
