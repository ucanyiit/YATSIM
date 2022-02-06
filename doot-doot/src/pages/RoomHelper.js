import type0 from '../assets/cells/type0.png';
import type1 from '../assets/cells/type1.png';
import type2 from '../assets/cells/type2.png';
import type32 from '../assets/cells/type32.png';
import type31 from '../assets/cells/type31.png';
import type41 from '../assets/cells/type41.png';
import type40 from '../assets/cells/type40.png';
import type50 from '../assets/cells/type50.png';
import type51 from '../assets/cells/type51.png';
import type52 from '../assets/cells/type52.png';
import type6 from '../assets/cells/type6.png';
import type7 from '../assets/cells/type7.png';
import type8 from '../assets/cells/type8.png';

import wagonType0 from '../assets/trains/type0.png';
import wagonType1 from '../assets/trains/type1.png';

const cellTable = {
  0: type0,
  1: type1,
  2: type2,
  3: {
    2: type32,
    1: type31,
  },
  4: {
    1: type41,
    0: type40,
  },
  5: {
    0: type50,
    1: type51,
    2: type52,
  },
  6: type6,
  7: type7,
  8: type8,
};

const wagonTable = {
  0: wagonType0,
  1: wagonType1,
};

export const getCellImage = (type, state = null) => {
  if (state) return cellTable[type][state];
  return cellTable[type];
};

export const getWagonImage = (type) => wagonTable[type];
