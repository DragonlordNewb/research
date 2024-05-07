#include "orbit.h"
#include <string>

using namespace std;

namespace cb {

    class CelestialBody {

        public:

            string name;
            double sgp;
            double radius;

            bool hasAtmosphere = false;
            double atmosphereHeight = -1;
            double lowestStableOrbit = -1;

            CelestialBody* parent;
            orbit::Orbit parentOrbit;
            double trueAnomaly;

            CelestialBody(string name, double sgp, double radius, double atmoheight=-1): name(name), sgp(sgp), radius(radius) {
                if (atmoheight != -1) {
                    hasAtmosphere = true;
                    atmosphereHeight = atmoheight;
                    lowestStableOrbit = radius + atmoheight;
                }
            }

            void placeInOrbit(CelestialBody parentBody, orbit::Orbit orbitAroundParent, double trueAnomalyAroundParent) {
                parent = &parentBody;
                parentOrbit = orbitAroundParent;
                trueAnomaly = trueAnomalyAroundParent;
            }

    };

};
