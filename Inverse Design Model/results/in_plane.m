
soil_params = xlsread('designed_parameters_in.xlsx', 'soil_parameters');
images = xlsread('designed_parameters_in.xlsx', 'designed_images');
as = xlsread('designed_parameters_in.xlsx', 'designed_periodic_constants');


for i=1:10
tic
i
name=i;
tu = reshape(images(i, :, :), [50, 50]);
Es = soil_params(i, 1)*1e6;
Ps = soil_params(i, 2);
rhos = soil_params(i, 3)*1e3;

try
    list_c = [];
    c = 1;
    for m=1:50
        for n=1:50
            if tu(m, n)==1
                list_c(c) = (n+50*(m-1));
                c = c+1;
            end
        end
    end

    model = mphload('in_plane.mph');
    filename = ['dispersion_curves_in/', num2str(i), '.csv'];

    model.param.set('Es', num2str(Es));
    model.param.set('Ps', num2str(Ps));
    model.param.set('rhos', num2str(rhos));

    model.component('comp1').physics('solid').feature('lemm2').selection.set(list_c);
    

    model.study('std1').run;


    %创建色散曲线
    model.result.create('pg2', 'PlotGroup1D');
    model.result('pg2').run;
    model.result('pg2').create('glob1', 'Global');
    model.result('pg2').feature('glob1').set('markerpos', 'datapoints');
    model.result('pg2').feature('glob1').set('linewidth', 'preference');
    model.result('pg2').feature('glob1').set('data', 'dset2');
    model.result('pg2').feature('glob1').set('expr', {'solid.freq'});
    model.result('pg2').feature('glob1').set('descr', {[native2unicode(hex2dec({'98' '91'}), 'unicode')  native2unicode(hex2dec({'73' '87'}), 'unicode') ]});
    model.result('pg2').feature('glob1').set('unit', {'Hz'});
    model.result('pg2').feature('glob1').set('xdatasolnumtype', 'outer');
    model.result('pg2').run;
    
    %导出色散曲线
    model.result.export.create('plot1', 'Plot');
    model.result.export('plot1').set('plotgroup', 'pg2');
    model.result.export('plot1').set('filename', filename);
    model.result.export('plot1').run;

    model.hist.disable;
%     mphsave(model, ['dispersion_curves/', num2str(i+num*n_excel)]);
catch
    dlmwrite([num2str(i), '.txt'], i);
end
toc
end
