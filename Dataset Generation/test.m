function out = model
%
% test.m
%
% Model exported on Jul 28 2024, 15:52 by COMSOL 6.1.0.282.

import com.comsol.model.*
import com.comsol.model.util.*

model = ModelUtil.create('Model');

model.modelPath(['C:\Users\15895\Desktop\' native2unicode(hex2dec({'8b' 'fe'}), 'unicode')  native2unicode(hex2dec({'7a' '0b'}), 'unicode') '\' native2unicode(hex2dec({'7b' '2c'}), 'unicode')  native2unicode(hex2dec({'4e' '8c'}), 'unicode')  native2unicode(hex2dec({'59' '29'}), 'unicode') '\' native2unicode(hex2dec({'62' 'd3'}), 'unicode')  native2unicode(hex2dec({'62' '51'}), 'unicode')  native2unicode(hex2dec({'53' 'd8'}), 'unicode')  native2unicode(hex2dec({'91' 'cf'}), 'unicode')  native2unicode(hex2dec({'65' '70'}), 'unicode')  native2unicode(hex2dec({'63' '6e'}), 'unicode')  native2unicode(hex2dec({'96' 'c6'}), 'unicode')  native2unicode(hex2dec({'75' '1f'}), 'unicode')  native2unicode(hex2dec({'62' '10'}), 'unicode') ]);

model.label('topology.mph');

model.param.set('k1', '1');
model.param.set('k2', '1');
model.param.set('a', '1[m]');
model.param.set('kx', 'k1*pi/a');
model.param.set('ky', 'k2*pi/a');
model.param.set('Es', '20e6');
model.param.set('Ps', '0.35');
model.param.set('rhos', '1900');
model.param.set('Ec', '30e9');
model.param.set('Pc', '0.2');
model.param.set('rhoc', '2500');

model.component.create('comp1', true);

model.component('comp1').geom.create('geom1', 2);

model.component('comp1').mesh.create('mesh1');

model.component('comp1').geom('geom1').create('sq1', 'Square');
model.component('comp1').geom('geom1').feature('sq1').set('size', 'a/50');
model.component('comp1').geom('geom1').create('arr1', 'Array');
model.component('comp1').geom('geom1').feature('arr1').set('fullsize', [50 50]);
model.component('comp1').geom('geom1').feature('arr1').set('displ', {'a/50' 'a/50'});
model.component('comp1').geom('geom1').feature('arr1').selection('input').set({'sq1'});
model.component('comp1').geom('geom1').run;

model.component('comp1').common.create('mpf1', 'ParticipationFactors');

model.component('comp1').physics.create('solid', 'SolidMechanics', 'geom1');
model.component('comp1').physics('solid').create('lemm2', 'LinearElasticModel', 2);
model.component('comp1').physics('solid').feature('lemm2').selection.set([205 206 207 255 256 257 305 306 307]);
model.component('comp1').physics('solid').create('pc1', 'PeriodicCondition', 1);
model.component('comp1').physics('solid').feature('pc1').selection.set([1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 41 43 45 47 49 51 53 55 57 59 61 63 65 67 69 71 73 75 77 79 81 83 85 87 89 91 93 95 97 99 5051 5052 5053 5054 5055 5056 5057 5058 5059 5060 5061 5062 5063 5064 5065 5066 5067 5068 5069 5070 5071 5072 5073 5074 5075 5076 5077 5078 5079 5080 5081 5082 5083 5084 5085 5086 5087 5088 5089 5090 5091 5092 5093 5094 5095 5096 5097 5098 5099 5100]);
model.component('comp1').physics('solid').create('pc2', 'PeriodicCondition', 1);
model.component('comp1').physics('solid').feature('pc2').selection.set([2 101 103 202 204 303 305 404 406 505 507 606 608 707 709 808 810 909 911 1010 1012 1111 1113 1212 1214 1313 1315 1414 1416 1515 1517 1616 1618 1717 1719 1818 1820 1919 1921 2020 2022 2121 2123 2222 2224 2323 2325 2424 2426 2525 2527 2626 2628 2727 2729 2828 2830 2929 2931 3030 3032 3131 3133 3232 3234 3333 3335 3434 3436 3535 3537 3636 3638 3737 3739 3838 3840 3939 3941 4040 4042 4141 4143 4242 4244 4343 4345 4444 4446 4545 4547 4646 4648 4747 4749 4848 4850 4949 4951 5050]);

model.component('comp1').view('view1').axis.set('xmin', -0.3064837157726288);
model.component('comp1').view('view1').axis.set('xmax', 1.3064836263656616);
model.component('comp1').view('view1').axis.set('ymin', -0.04999998211860657);
model.component('comp1').view('view1').axis.set('ymax', 1.0499999523162842);

model.component('comp1').physics('solid').feature('lemm1').set('E_mat', 'userdef');
model.component('comp1').physics('solid').feature('lemm1').set('E', 'Es');
model.component('comp1').physics('solid').feature('lemm1').set('nu_mat', 'userdef');
model.component('comp1').physics('solid').feature('lemm1').set('nu', 'Ps');
model.component('comp1').physics('solid').feature('lemm1').set('rho_mat', 'userdef');
model.component('comp1').physics('solid').feature('lemm1').set('rho', 'rhos');
model.component('comp1').physics('solid').feature('lemm1').label('soil');
model.component('comp1').physics('solid').feature('lemm2').set('E_mat', 'userdef');
model.component('comp1').physics('solid').feature('lemm2').set('E', 'Ec');
model.component('comp1').physics('solid').feature('lemm2').set('nu_mat', 'userdef');
model.component('comp1').physics('solid').feature('lemm2').set('nu', 'Pc');
model.component('comp1').physics('solid').feature('lemm2').set('rho_mat', 'userdef');
model.component('comp1').physics('solid').feature('lemm2').set('rho', 'rhoc');
model.component('comp1').physics('solid').feature('lemm2').label('concrete');
model.component('comp1').physics('solid').feature('pc1').set('PeriodicType', 'Floquet');
model.component('comp1').physics('solid').feature('pc1').set('kFloquet', {'kx'; 'ky'; '0'});
model.component('comp1').physics('solid').feature('pc2').set('PeriodicType', 'Floquet');
model.component('comp1').physics('solid').feature('pc2').set('kFloquet', {'kx'; 'ky'; '0'});

model.study.create('std1');
model.study('std1').create('param', 'Parametric');
model.study('std1').create('eig', 'Eigenfrequency');
model.study('std1').feature('param').set('pname', {'k1' 'k2'});
model.study('std1').feature('param').set('plistarr', {'range(1,-0.1,0) range(0.1,0.1,1) 1 1 1 1 1 1 1 1 1 1' 'range(1,-0.1,0) 0 0 0 0 0 0 0 0 0 0 range(0.1,0.1,1)'});
model.study('std1').feature('param').set('punit', {'' ''});

out = model;
