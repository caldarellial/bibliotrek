import { defaultConfig } from "@tamagui/config/v5";
import { createAnimations } from "@tamagui/animations-react-native";
import { createTamagui } from "tamagui";

import { themes } from "./themes";

export const config = createTamagui({
  ...defaultConfig,
  themes,
  animations: createAnimations({
    bouncy: {
      damping: 10,
      mass: 0.9,
      stiffness: 100,
    },
    lazy: {
      damping: 18,
      stiffness: 50,
    },
    lazyBounce: {
      damping: 6,
      mass: 0.8,
      stiffness: 30,
    },
    quick: {
      damping: 20,
      mass: 1.2,
      stiffness: 250,
    },
  }),
});
