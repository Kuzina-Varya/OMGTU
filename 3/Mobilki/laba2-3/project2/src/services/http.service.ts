//npm install axios
//npm install --save-dev @types/axios 
//npm install --save-dev @types/node
// src/services/http.service.ts
import axios, { AxiosInstance } from 'axios';
import * as t from 'io-ts';
import { decodeOrThrow } from '@/utils/decode';

class HttpService {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({ baseURL });
  }

  async get<T>(url: string, codec: t.Type<T>, params?: Record<string, unknown>): Promise<T> {
    const res = await this.client.get(url, { params });
    return decodeOrThrow(codec, res.data);
  }
}

export const nobelApi = new HttpService('/api/v1');