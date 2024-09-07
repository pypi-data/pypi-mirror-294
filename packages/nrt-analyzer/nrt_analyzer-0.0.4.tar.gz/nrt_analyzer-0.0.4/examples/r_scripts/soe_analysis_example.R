library(RSQLite)
library(ggplot2)
library(dplyr)
library(purrr)
library(tidyr)
library(ggrepel)
library(lme4)
library(lmerTest)
library(LMERConvenienceFunctions)
library(varhandle)
library(optimx)
library(effects)
library(magrittr)
library(sjPlot)
formater <- (theme_bw() +  
               theme(axis.line = element_line(colour = "black"),
                     panel.grid.major = element_blank(),
                     panel.grid.minor = element_blank(),
                     panel.border = element_blank(),
                     panel.background = element_blank()) + 
               theme(legend.text=element_text(size=6)) +
               theme(legend.title = element_text(size=8)) +
               theme(axis.line.x = element_line(color="black", size = 0.2), axis.line.y = element_line(color="black", size = 0.2)) +
               theme(strip.background = element_blank()) + 
               theme(plot.title = element_text(hjust = 0.5))+
               theme(plot.subtitle = element_text(size = 8)) 
)

figures_path = "/run/media/jundurraga/Elements/Measurements/CINGT/NRT/figures/"
data_base_path = '/run/media/jundurraga/Elements/Measurements/CINGT/NRT/data.sqlite'

con = dbConnect(drv=SQLite(), dbname = data_base_path)
alltables = dbListTables(con)
all_data = dbGetQuery(con, "
                      SELECT S.subject_id,
                      S.anonymous_name,
                      MI.experiment,
                      MI.condition,
                      MI.date,
                      STI.*,
                      SOE.*
                      FROM subjects as S
                      JOIN measurement_info MI ON (MI.id_subject = S.id)
                      JOIN stimuli STI ON STI.id_measurement = MI.id
                      JOIN recording REC ON REC.id_stimuli = STI.id
                      JOIN soe_measures SOE ON SOE.id_stimuli = STI.id")
dbDisconnect(con)

all_data %<>% 
  map_if(., .p = function(x) all(check.numeric(x)), .f = as.numeric, .else = factor) %>%
  as.data.frame(.) 


gp_centroid <- all_data %>% 
  ggplot(aes(Masker_Active_Electrode, centroid, color=probe_mode)) +
  geom_point() +
  ylab("Centroid [electrodes]") +
  xlab("Active Electrode") + 
  formater
gp_centroid

ggsave(plot = gp_centroid, paste(figures_path, "soe_centroid.png", sep=""),  width = 14,  height = 20, units = "cm")


gp_width <- all_data %>% 
  ggplot(aes(Masker_Active_Electrode, width, color=probe_mode)) +
  geom_point() +
  ylab("Width [electrodes]") +
  xlab("Active Electrode") + 
  formater
gp_width

ggsave(plot = gp_width, paste(figures_path, "soe_width.png", sep=""),  width = 14,  height = 20, units = "cm")

