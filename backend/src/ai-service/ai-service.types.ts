export interface BuscarContextoRequest {
  pergunta: string;
  curso?: string;
  perfil?: string;
  top_k?: number;
}

export interface FonteContexto {
  arquivo: string;
  pagina: number;
  curso: string;
}

export interface BuscarContextoResponse {
  contexto: string;
  fontes: FonteContexto[];
  distancia_minima: number;
}
