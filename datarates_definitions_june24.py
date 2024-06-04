#print(buffersize_gbps)
gbps_to_PB=(1/(8000*1e3))
gbps_to_TB=(1/(8000))
def visibility_size_low(number_stations,n_chan,obs_time,int_time,freq_res):
    n_baselines=(number_stations*(number_stations+1))/2
    default_time_res=0.85
    n_rows = n_baselines * int( obs_time / int_time)
    #default_time_res=0.85 
    default_frequency=5.4e3 #default frequency resolution =5.4kHz
    frequency_scaling=freq_res/default_frequency
    n_chan=n_chan/(frequency_scaling)
    #4 polarizations already taken into account.
    sb_size = n_rows * ((7*8) + (4+(4*n_chan)) + (4*11) + (8*1) + (4) + (4 * (8 + 8*n_chan + 4*n_chan)))
    sGB=(1024*1024*1024)
    sTB=(1024*1024*1024*1024)
    sPB=(1024*1024*1024*1024*1024)
    print(f'visib size {round(sb_size/sGB,3)}GB,{round(sb_size/sTB,4)}TB,{round(sb_size/sPB,4)}PB')
    return sb_size/sTB

def image_size_low(station_diameter,max_baseline_length,n_chan_image,n_pols,n_products,number_beams):
    image_size=7.5*(max_baseline_length/station_diameter)**2 * (32/8)
    #Assuming 4 imaging products, image, model, residual, psf (1 channel only)
    final_cube= number_beams * n_pols * n_chan_image * image_size *(n_products-1) + (number_beams*image_size) #last part is the PSF which will be 1 channel
    sGB=(1024*1024*1024)
    sTB=(1024*1024*1024*1024)
    sPB=(1024*1024*1024*1024*1024)
    print(f'cube size {round(final_cube/sGB,4)}GB, {round(final_cube/sTB,10)}TB,{round(final_cube/sPB,6)}PB')
    totalTB=final_cube/sTB
    return totalTB

def contimage_size_low(station_diameter,max_baseline_length,n_pols,n_products,number_beams):
    image_size=7.5*(max_baseline_length/station_diameter)**2 * (32/8)
    #Assuming 4 imaging products, image, model, residual, psf ( all 1 channel only as an mfs image)
    n_chan_image=1
    #Assuming 11 images are made to be able to do spectral index?
    final_cube= 11 * number_beams * n_pols * n_chan_image * image_size * n_products
    sGB=(1024*1024*1024)
    sTB=(1024*1024*1024*1024)
    sPB=(1024*1024*1024*1024*1024)
    print(f'Continuum images size {round(final_cube/sGB,4)}GB, {round(final_cube/sTB,10)}TB,{round(final_cube/sPB,6)}PB')
    totalTB=final_cube/sTB
    return totalTB


def pss(assumed_TB,pss_beams):
    if assumed_TB>0:
        print('PSS',assumed_TB)
        assumed_pss=assumed_TB
    else: #PSS
        #assume 50% of the 1000 detections will be sent?
        n_det=0.5
        data_packets=6 #minute chunks
        number_hours=4
        dp=60/data_packets*number_hours
        datasize_pss=0.0839*100 *pss_beams # Gb/sdatasize packets for a given bin sent assuming 1000 detections processed
        assumed_pss=datasize_pss*gbps_to_TB * dp * n_det #assuming data will be averaged over 10 minutes chunks so 40 in 4 hours
        #assume 50% of the 1000 detections will be sent?

        print('PSS',assumed_pss,'TB')
    return assumed_pss


def pst(number_beams_pst,obs_time):
    datarate=2*1.33 
    assumed_pst=number_beams_pst*datarate*obs_time*gbps_to_TB
    print('PST=',round(assumed_pst,3),'TB')
    return assumed_pst

def transient_buffer(number_stations,number_beams,number_hours,events_per_hour):
    buffersize_gbps=(192 * 2 * number_stations * (1/1e-6))/1e9 #bps
    buffersize=buffersize_gbps*gbps_to_TB*events_per_hour*60*number_hours*number_beams
    print('Transient Buffersize',buffersize,'TB')
    return buffersize

def dynamic_spectrum(number_beams_pst,obs_time):
    datarate=2.048  #Gb/s
    dynamic_TB=number_beams_pst*datarate*obs_time*gbps_to_TB
    print('Dynamic spectrum',dynamic_TB,'TB')
    return dynamic_TB

def flowthrough_mode(number_beams_pst,obs_time):
    datarate=1.92 #Gb/s
    flowthrough=number_beams_pst*datarate*obs_time*gbps_to_TB
    print('Flowthrough=',flowthrough,'TB')
    return flowthrough
