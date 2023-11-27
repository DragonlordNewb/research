#pragma once

#include "../util/vec3.h"
#include "field.h"

class Property {

	public:

		std::string name;
		double value;

		Property(string name_, double value_): name(name_), value(value_) {}

		double get() {
			return value;
		}

};

class QuantumWave {

	public:

		Property* properties;
		Field<complex<double>> position;
		Field<complex<double>> velocity;

		QuantumWave(Vec3 size, double resolution, Property properties_[], int propertyCount) {
			properties = new Property[propertyCount]
			for (int i = 0; i < propertyCount; i++) {
				properties[i] = properties_[i];
			}
			position.initialize(size, resolution);
			velocity.initialize(size, resolution);
		}

		complex<double> positionAmplitude(Vec3 v) {
			return position.get(v);
		}

		complex<double> velocityAmplitude(Vec3 v) {
			return velocity.get(v);
		}

		double positionProbability(Vec3 v) {
			double absolute = abs(positionAmplitude(v));
			return absolute * absolute;
		}

		double velocityProbability(Vec3 v) {
			double absolute = abs(velocityAmplitude(v));
			return absolute * absolute;
		}

};