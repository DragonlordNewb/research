#include "utils.cpp"
#include "constants.cpp"

using namespace std;

class Atom {

	public:	

		double restMass;
		map<string, double> charges;

		Vec3 position;
		Vec3 velocity;
		Vec3 rotation;
		Vec3 spin;	

		Atom(
				int _id; 
				double _restMass, 
				map<string, double> _charges, 
				Vec3 _position=Vec3(), 
				Vec3 _velocity=Vec3(),
				Vec3 _rotation=Vec3(),
				Vec3 _spin=Vec3()) {
			id = _id;
			restMass = _restMass;
			position = _position;
			velocity = _velocity;
			rotation = _rotation;
			spin = _spin;
		}

		Atom() {}

		double gamma() {
			double beta = velocity.magnitude() / c;
			return 1 / sqrt(1 - (beta * beta));
		}

		double mass() {
			return restMass * gamma();
		}

};

class Entity {

	public:

		int id;
		double restMass;
		map<string, double> charges;

		Vec3 position;
		Vec3 velocity;
		Vec3 rotation;
		Vec3 spin;

		Entity(
				int _id; 
				double _restMass, 
				map<string, double> _charges, 
				Vec3 _position=Vec3(), 
				Vec3 _velocity=Vec3(),
				Vec3 _rotation=Vec3(),
				Vec3 _spin=Vec3()) {
			id = _id;
			restMass = _restMass;
			position = _position;
			velocity = _velocity;
			rotation = _rotation;
			spin = _spin;
		}

		virtual vector<Atom> atoms() = 0;

		double gamma() {
			double beta = velocity.magnitude() / c;
			return 1 / sqrt(1 - (beta * beta));
		}

		double mass() {
			return restMass * gamma();
		}

		double rotationalInertia(Vec3 axis) {
			vector<Atom> atoms_ = atoms();
			double I = 0;
			Atom atom;
			double r;

			for (int i = 0; i < atoms_.size(); i++) {
				atom = atoms_[i];
				r = atom.position.dot(axis) / axis.magnitude();
				I += atom.mass() / r;
			}

			return I;
		}

};