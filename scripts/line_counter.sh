#pygount --suffix=py,js,css,html,json,scss,md,sh,txt,ini,cfg --format=summary --folders-to-skip venv,jquery,bootstrap,swiper,vue,sortable,clockpicker,hammer,iconify,live,range-slider,test,chartjs,socket,popper,animate,apexcharts
echo "============================================="
echo "                    Full"
echo "============================================="
echo ""
pygount --suffix=py,js,css,html --format=summary --folders-to-skip venv,jquery,bootstrap,swiper,vue,sortable,clockpicker,hammer,iconify,live,range-slider,test,chartjs,socket,popper,animate,apexcharts,moment,fotorama,test_files
echo ""
echo ""
echo "============================================="
echo "                   Dynamic"
echo "============================================="
echo ""
pygount --suffix=py,js,css,html --format=summary --folders-to-skip venv,jquery,bootstrap,swiper,vue,sortable,clockpicker,hammer,iconify,live,range-slider,test,chartjs,socket,popper,animate,apexcharts,moment,fotorama,test_files,items,tiles,config,data,scripts
echo ""
