#include "util.h"

namespace orbit {

    enum OrbitType { Escape, Parking, Reentry, Aerobrake, Collision };

    struct Situation(
        string body;
        OrbitType orbitType;
    )

    class Orbit {

        public:

            double sgp;
            double centralBodyMass;
            
            vecs::XYZ specificAngularMomentum;
            double specificOrbitalEnergy;
            
            double semiMajorAxis;
            double semiMinorAxis;
            double semiLatusRectum;
            double eccentricity;
            double apoapsis;
            double periapsis;
            
            double inclination;
            double ascendingNodeLongitude;

            Orbit() {}
            
            Orbit(double sgp, vecs::XYZ r, vecs::XYZ v): sgp(sgp), centralBodyMass(sgp / consts::G) {
                specificOrbitalEnergy = (v.getLength() / 2) - (sgp / r.getLength());
                specificAngularMomentum = vecs::XYZ::cross(r, v);
                calculateOrbitalParameters();
            }

            Orbit(double sgp, vecs::RThetaPhi rrtp, vecs::RThetaPhi vrtp): sgp(sgp), centralBodyMass(sgp / consts::G) {
                vecs::XYZ r = vecs::sphericalToRectangular(rrtp);
                vecs::XYZ v = vecs::sphericalToRectangular(vrtp);
                specificOrbitalEnergy = (v.getLength() / 2) - (sgp / r.getLength());
                specificAngularMomentum = vecs::XYZ::cross(r, v);
                calculateOrbitalParameters();
            }

            Orbit(double sgp, vecs::RThetaZ rrtz, vecs::RThetaZ vrtz): sgp(sgp), centralBodyMass(sgp / consts::G) {
                vecs::XYZ r = vecs::cylindricalToRectangular(rrtz);
                vecs::XYZ v = vecs::cylindricalToRectangular(vrtz);
                specificOrbitalEnergy = (v.getLength() / 2) - (sgp / r.getLength());
                specificAngularMomentum = vecs::XYZ::cross(r, v);
                calculateOrbitalParameters();
            }

            void calculateOrbitalParameters() {
                eccentricity = sqrt(
                    1 + (
                        (2 * specificOrbitalEnergy * pow(specificAngularMomentum.getLength(), 2))
                        / pow(sgp, 2)
                    )
                );
                semiMajorAxis = -1 * (sgp / (2 * specificOrbitalEnergy));
                semiMinorAxis = semiMajorAxis * sqrt(1 - pow(eccentricity, 2));
                semiLatusRectum = semiMajorAxis * (1 - pow(eccentricity, 2));
                
                apoapsis = semiMajorAxis * (1 + eccentricity);
                periapsis = semiMajorAxis * (1 - eccentricity);
                
                inclination = acos(specificAngularMomentum.z / specificAngularMomentum.getLength());
                vecs::XYZ n(-1 * specificAngularMomentum.y, specificAngularMomentum.x, 0);
                if (n.y >= 0) {
                    ascendingNodeLongitude = acos(n.x / n.getLength());
                } else {
                    ascendingNodeLongitude = (2 * consts::pi) - acos(n.x / n.getLength());
                }
                
            }

            double calculateInstantaneousDistance(double angle) {
                return (semiLatusRectum / (1 + (eccentricity * cos(angle))));
            }

            double calculateInstantaneousVelocity(double angle) {
                double r = calculateInstantaneousDistance(angle);
                return (sqrt(sgp * ((2 / r) - (1 / semiMajorAxis))));
            }

    };

};