#pragma once

#include "../util/vec3.h"
#include "../util/const.h"

class Field {

	public:

		double*** data;
		double resolution;

		Vec3 size;
		int xlen;
		int ylen;
		int zlen;

		Field(Vec3 size_, double resolution_): 
				size(size_),
				xlen((int)(size.x / resolution)),
				ylen((int)(size.y / resolution)),
				zlen((int)(size.z / resolution)) {
			
			data = new double**[xlen];
			for (int x = 0; x < xlen; x++) {
				data[x] = new double*[ylen];
				for (int y = 0; y < ylen; y++) {
					data[x][y] = new double[zlen];
					for (int z = 0; z < zlen; z++) {
						data[x][y][z] = (double)(0);
					}
				}
			}

		}

		double get(double x, double y, double z) {
			int xl = (int)(x / resolution);
			int yl = (int)(y / resolution);
			int zl = (int)(z / resolution);

			return data[xl][yl][zl];
		}

		inline double get(Vec3 v) {
			return get(v.x, v.y, v.z);
		}

		void set(double x, double y, double z, double value) {
			int xl = (int)(x / resolution);
			int yl = (int)(y / resolution);
			int zl = (int)(z / resolution);

			data[xl][yl][zl] = value;
		}

		void set(Vec3 v, double value) {
			set(v.x, v.y, v.z, value);
		}

};

namespace inits {

	// as it turns out, in n dimensions, the integral over n-space
	// of any properly Gaussian/normal distribution is equal to 
	// pi ^ (n-1)/2. In two dimensions, for example, a Gaussian
	// function f(x) has an integral S f(x) dx = pi ^ 1/2. In three
	// dimensions, a Gaussian function g(x,y) has an integral
	// S g(x,y) dx dy = pi. Similarly, in four dimensions, a Gaussian
	// function h(x,y,z) has an integral S h(x,y,z) dx dy dz = pi^(3/2).
	//
	// By dividing by pi^(3/2), the function is normalized to have
	// an integral of 1.

	const double GAUSSIAN_NORMALIZATION_3D = (double)(0.5) / (constant::pi * constant::pi * std::sqrt(constant::pi));

	double gaussian3D(Vec3 v, Vec3 mu=Vec3(), double sigma=1) {
		return GAUSSIAN_NORMALIZATION_3D * std::exp((double)(-0.5) * ((v - mu) / sigma).length2());
	}

	void initGaussian(Field field, Vec3 mu=Vec3(), double sigma=1) {
		for (double x = 0; x <= field.size.x; x += field.resolution) {
			for (double y = 0; y <= field.size.x; y += field.resolution) {
				for (double z = 0; z <= field.size.x; z += field.resolution) {
					field.set(x, y, z, gaussian3D(Vec3(x, y, z), mu, sigma));
				}
			}
		}
	}

};