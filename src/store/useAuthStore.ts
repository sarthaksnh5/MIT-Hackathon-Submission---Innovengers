import {create} from 'zustand';
import {persist} from 'zustand/middleware';
import {zustandAsyncStorage} from './zustandAsyncStorage';

export type Organisation = {
  id: string;
  logo: string | null;
  name: string;
  email: string;
  primary_color: string;
  secondary_color: string;
};

type AuthState = {
  isLoggedIn: boolean;
  accessToken: string | null;
  refreshToken: string | null;
  login: (data: {access_token: string; refresh_token: string}) => void;
  logout: () => void;
  setTokens: (accessToken: string, refreshToken: string) => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    set => ({
      isLoggedIn: false,
      accessToken: null,
      refreshToken: null,
      organisations: [],
      selectedOrganisation: null,

      login: ({access_token, refresh_token}) =>
        set({
          isLoggedIn: true,
          accessToken: access_token,
          refreshToken: refresh_token,
        }),

      logout: () =>
        set({
          isLoggedIn: false,
          accessToken: null,
          refreshToken: null,
        }),

      setTokens: (accessToken, refreshToken) =>
        set({
          accessToken,
          refreshToken,
          isLoggedIn: !!accessToken,
        }),
    }),
    {
      name: 'auth-storage', // stored with AsyncStorage
      storage: zustandAsyncStorage,
    },
  ),
);
