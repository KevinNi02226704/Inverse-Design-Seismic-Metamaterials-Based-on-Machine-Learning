start_num = 1;
end_num = 2; 
n_excel = 2;

num = 0;

% 清空 dispersion_curves 目录
dispersion_dir = 'dispersion_curves';
if exist(dispersion_dir, 'dir')  % 检查目录是否存在
    delete(fullfile(dispersion_dir, '*'));  % 删除所有文件
end

% 使用 readmatrix 读取 Excel 文件
images = readmatrix(['integrated_images/', num2str(num), '.xlsx'], 'Sheet', 'images');
images = reshape(images, [2, 50, 50]);
soil_parameters = readmatrix(['integrated_images/', num2str(num), '.xlsx'], 'Sheet', 'soil_parameters');

for i=start_num:end_num
    tic
    i
    name = i;
    tu = reshape(images(i, :, :), [50, 50]);
    Es = soil_parameters(i, 1) * 1e6;
    Ps = soil_parameters(i, 2);
    rhos = soil_parameters(i, 3) * 1e3;

    try
        list_c = [];
        c = 1;
        for m = 1:50
            for n = 1:50
                if tu(m, n) == 1
                    list_c(c) = (n + 50 * (m - 1));
                    c = c + 1;
                end
            end
        end

        model = mphload('topology.mph');
        filename = ['dispersion_curves/', num2str(i), '.csv'];

        model.param.set('Es', num2str(Es));
        model.param.set('Ps', num2str(Ps));
        model.param.set('rhos', num2str(rhos));

        model.component('comp1').physics('solid').feature('lemm2').selection.set(list_c);

        model.study('std1').run;

        % 创建色散曲线
        model.result.create('pg2', 'PlotGroup1D');
        model.result('pg2').run;
        model.result('pg2').create('glob1', 'Global');
        model.result('pg2').feature('glob1').set('markerpos', 'datapoints');
        model.result('pg2').feature('glob1').set('linewidth', 'preference');
        model.result('pg2').feature('glob1').set('data', 'dset2');
        model.result('pg2').feature('glob1').set('expr', {'solid.freq'});
        model.result('pg2').feature('glob1').set('unit', {'Hz'});
        model.result('pg2').feature('glob1').set('xdatasolnumtype', 'outer');
        model.result('pg2').run;

        % 导出色散曲线
        model.result.export.create('plot1', 'Plot');
        model.result.export('plot1').set('plotgroup', 'pg2');
        model.result.export('plot1').set('filename', filename);
        model.result.export('plot1').run;

        model.hist.disable;

        % 使用 writematrix 代替 dlmwrite
        writematrix(i + num * n_excel, ['processing/', num2str(start_num + num * n_excel), 'to', num2str(end_num + num * n_excel), 'processing.txt']);

    catch
        % 使用 writematrix 代替 dlmwrite
        writematrix(i + num * n_excel, ['errors/', num2str(i + num * n_excel), '.txt']);

        % 仅在发生错误时保存 .mph 文件
        mphsave(model, ['dispersion_curves/error_', num2str(i + num * n_excel), '.mph']);
    end
    toc
end
