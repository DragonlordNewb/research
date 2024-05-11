#pragma once
#include <cmath>

namespace consts {
    const double c = 299792458;
    const double G = 6.6743e-11;
    const double pi = 3.14159265358979;
}

namespace uniconv {
    double m2km(double m) { return m / 1000; }
    double m2Mm(double m) { return m / 1000000; }
    double km2Mm(double km) { return km / 1000; }
    double m2AU(double m) { return m / 149598073000; }
    double km2AU(double km) { return km / 149598073; }
    double Mm2AU(double Mm) { return Mm / 149598.073; }
    double m2ly(double m) { return m / 9460730472580800; }
    double km2ly(double km) { return km / 9460730472580.8; }
}

namespace vecs {

    // 3 different types of vectors: rectangular, spherical, cylindrical

    class XYZ {

        public:

            double x;
            double y;
            double z;

            XYZ(): x(0), y(0), z(0) {}

            XYZ(double x, double y, double z): x(x), y(y), z(z) {}

            XYZ operator+(XYZ other) { return XYZ(x + other.x, y + other.y, z + other.z); }
            XYZ operator-(XYZ other) { return XYZ(x - other.x, y - other.y, z - other.z); }
            XYZ operator*(double k) { return XYZ(x * k, y * k, z * k); }
            XYZ operator/(double k) { return XYZ(x / k, y / k, z / k); }

            static double dot(XYZ a, XYZ b) { return (a.x * b.x) + (a.y * b.y) + (a.z * b.y); }
            static XYZ cross(XYZ a, XYZ b) {
                return XYZ(
                    (a.y * b.z) - (a.z * b.y),
                    (a.x * b.z) - (a.z * b.x),
                    (a.x * b.y) - (a.y * b.x)
                );
            }
            
            double getLength() { return sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2)); }

    };

    using Rectangular = XYZ;

    class RThetaPhi {

        public:

            double r;
            double theta;
            double phi;
            
            RThetaPhi(): r(0), theta(0), phi(0) {}

            RThetaPhi(double r, double theta, double phi): r(r), theta(theta), phi(phi) {}

            RThetaPhi operator+(RThetaPhi other) { return RThetaPhi(r + other.r, theta + other.theta, phi + other.phi); }
            RThetaPhi operator-(RThetaPhi other) { return RThetaPhi(r - other.r, theta - other.theta, phi - other.phi); }
            RThetaPhi operator*(double k) { return RThetaPhi(r * k, theta * k, phi * k); }
            RThetaPhi operator/(double k) { return RThetaPhi(r / k, theta / k, phi / k); }

    };

    using Spherical = RThetaPhi;

    class RThetaZ {

        public:

            double r;
            double theta;
            double z;

            RThetaZ(): r(0), theta(0), z(0) {}

            RThetaZ(double r, double theta, double z): r(r), theta(theta), z(z) {}

            RThetaZ operator+(RThetaZ other) { return RThetaZ(r + other.r, theta + other.theta, z + other.z); }
            RThetaZ operator-(RThetaZ other) { return RThetaZ(r - other.r, theta - other.theta, z - other.z); }
            RThetaZ operator*(double k) { return RThetaZ(r * k, theta * k, z * k); }
            RThetaZ operator/(double k) { return RThetaZ(r / k, theta / k, z / k); }

    };

    using Cylindrical = RThetaZ;

    // Conversions between the three

    XYZ sphericalToRectangular(RThetaPhi spherical) {
        return XYZ(
            spherical.r * sin(spherical.phi) * cos(spherical.theta),
            spherical.r * sin(spherical.phi) * sin(spherical.theta),
            spherical.r * cos(spherical.phi)
        );
    }

    XYZ cylindricalToRectangular(RThetaZ cylindrical) {
        return XYZ(
            cylindrical.r * cos(cylindrical.theta),
            cylindrical.r * sin(cylindrical.theta),
            cylindrical.z
        );
    }

    RThetaPhi rectangularToSpherical(XYZ rectangular) {
        return RThetaPhi(
            rectangular.getLength(),
            atan(rectangular.y / rectangular.x),
            acos(rectangular.z / rectangular.getLength())
        );
    }

    RThetaPhi cylindricalToSpherical(RThetaZ cylindrical) {
        return RThetaPhi(
            sqrt(pow(cylindrical.r, 2) + pow(cylindrical.z, 2)),
            cylindrical.theta,
            acos(cylindrical.z / sqrt(pow(cylindrical.r, 2) + pow(cylindrical.z, 2)))
        );
    }

    RThetaZ rectangularToCylindrical(XYZ rectangular) {
        return RThetaZ(
            sqrt(pow(rectangular.x, 2) + pow(rectangular.y, 2)),
            atan(rectangular.y / rectangular.x),
            rectangular.z
        );
    }

    RThetaZ sphericalToCylindrical(RThetaPhi spherical) {
        return RThetaZ(
            spherical.r * sin(spherical.phi),
            spherical.theta,
            spherical.r * cos(spherical.phi)
        );
    }

};