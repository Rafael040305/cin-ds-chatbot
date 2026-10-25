import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from './../src/app.module.js';
import { OrchestrationService } from '../src/orchestration/orchestration.service.js';

describe('AppController (e2e)', () => {
  let app: INestApplication<App>;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/ (GET)', () => {
    return request(app.getHttpServer())
      .get('/')
      .expect(200)
      .expect('Hello World!');
  });

  it('/api/v1/conversa (POST) - consulta inválida', () => {
  return request(app.getHttpServer())
    .post('/api/v1/conversa')
    .send({
      consulta: {
        pergunta: '',
      },
    })
    .expect(400);
});
it('/api/v1/conversa (POST) - retorna contexto e fontes', async () => {
  const resultadoSimulado = {
    contexto: 'Trecho de uma norma sobre dispensa.',
    fontes: [
      {
        arquivo: 'norma-dispensa.pdf',
        pagina: 3,
        curso: 'CC',
      },
    ],
    distancia_minima: 0.2,
    fallback_acionado: false,
  };

  const processar = vi
    .spyOn(app.get(OrchestrationService), 'processar')
    .mockResolvedValueOnce(resultadoSimulado);

    try {
    await request(app.getHttpServer())
      .post('/api/v1/conversa')
      .send({
        consulta: {
          pergunta: 'Como solicitar dispensa?',
          curso: 'CC',
        },
      })
      .expect(201)
      .expect(resultadoSimulado);

    expect(processar).toHaveBeenCalledWith({
      consulta: {
        pergunta: 'Como solicitar dispensa?',
        curso: 'CC',
      },
    });
  } finally {
    processar.mockRestore();
  }
});

it('/api/v1/conversa (POST) - retorna fallback', async () => {
  const resultadoSimulado = {
    contexto: '',
    fontes: [],
    distancia_minima: 1,
    fallback_acionado: true as const,
    setor_sugerido: 'SecGrad' as const,
    template_email: 'Assunto: Dispensa\n\nOlá, gostaria de orientação.',
  };

  const processar = vi
    .spyOn(app.get(OrchestrationService), 'processar')
    .mockResolvedValueOnce(resultadoSimulado);

  try {
    await request(app.getHttpServer())
      .post('/api/v1/conversa')
      .send({
        consulta: {
          pergunta: 'Como solicitar dispensa?',
          curso: 'CC',
        },
      })
      .expect(201)
      .expect(resultadoSimulado);

    expect(processar).toHaveBeenCalledWith({
      consulta: {
        pergunta: 'Como solicitar dispensa?',
        curso: 'CC',
      },
    });
  } finally {
    processar.mockRestore();
  }
});

  afterEach(async () => {
    await app.close();
  });
});
