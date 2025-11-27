// src/utils/decode.ts
import { Either, fold } from 'fp-ts/Either';
import * as t from 'io-ts';

export function decodeOrThrow<T>(codec: t.Type<T>, input: unknown): T {
  const decoded: Either<t.Errors, T> = codec.decode(input);

  return fold<t.Errors, T, T>(
    (errors) => {
      const errorMessage = `Validation failed:\n${JSON.stringify(errors, null, 2)}`;
      console.error(errorMessage);
      throw new Error(errorMessage);
    },
    (data) => data
  )(decoded);
}