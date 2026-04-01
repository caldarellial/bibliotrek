import { IntroScreen } from "features/intro";
import { useRouter } from "expo-router";
import { useExistingAuth } from "features/auth";

export default function Index() {
  const router = useRouter();
  const existingAuth = useExistingAuth();
  return (
    <IntroScreen
      onComplete={() => {
        existingAuth(
          () => {
            router.push("/main");
          },
          () => {
            router.push("/auth");
          },
        );
      }}
    />
  );
}
