import { createContext, type ReactNode, useContext, useState } from "react";

type AuthContextType = {
	token: string | null;
	login: (token: string) => void;
	logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
	const [token, setToken] = useState<string | null>(
		localStorage.getItem("token"),
	);

	const login = (t: string) => {
		setToken(t);
		localStorage.setItem("token", t);
	};

	const logout = () => {
		setToken(null);
		localStorage.removeItem("token");
	};

	return (
		<AuthContext.Provider value={{ token, login, logout }}>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => {
	const ctx = useContext(AuthContext);
	if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
	return ctx;
};
