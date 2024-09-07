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

getCurrentFileLocation <-  function()
{
  this_file <- commandArgs() %>%
    tibble::enframe(name = NULL) %>%
    tidyr::separate(col=value, into=c("key", "value"), sep="=", fill='right') %>%
    dplyr::filter(key == "--file") %>%
    dplyr::pull(value)
  if (length(this_file)==0)
  {
    this_file <- rstudioapi::getSourceEditorContext()$path
  }
  return(dirname(this_file))
}


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

# Set path
setwd(getCurrentFileLocation())

figures_path = "./figures/"
database_path = '../../test_data/data.sqlite'

con = dbConnect(drv=SQLite(), dbname = database_path)
alltables = dbListTables(con)
all_data = dbGetQuery(con, "
                      SELECT S.subject_id,
                      S.anonymous_name,
                      MI.experiment,
                      MI.condition,
                      MI.date,
                      STI.*,
                      Amp.*
                      FROM subjects as S
                      JOIN measurement_info MI ON (MI.id_subject = S.id)
                      JOIN stimuli STI ON STI.id_measurement = MI.id
                      JOIN recording REC ON REC.id_stimuli = STI.id
                      JOIN amplitudes Amp ON Amp.id_stimuli = STI.id")
dbDisconnect(con)

all_data %<>% 
  map_if(., .p = function(x) all(check.numeric(x)), .f = as.numeric, .else = factor) %>%
  as.data.frame(.) %>%
  dplyr::mutate(amp_sig = factor(amp_sig),
                rate = factor(Probe_Rate))
  
all_data <- na.omit(all_data)

gp_agp <- all_data %>% 
  dplyr::filter(measurement_type == "AGF") %>%
  dplyr::group_by(probe_mode, Probe_Active_Electrode, Probe_Rate) %>%
  ggplot(aes(Probe_Current_Level, N1_P2_amp, 
             ymin=N1_P2_amp - amp_ci/2,
             ymax=N1_P2_amp + amp_ci/2, 
             color=paste(rate), 
             group=paste(Probe_Active_Electrode, rate))) +
  geom_point() +
  geom_errorbar() +
  geom_line() + 
  facet_grid(Probe_Active_Electrode ~ probe_mode) +
  ylab("Amplitude [uV]") +
  xlab("Current Units") + 
  formater +
  guides(color=guide_legend(title="Rate"))
gp_agp

ggsave(plot = gp_agp, paste(figures_path, "agf.png", sep=""),  width = 14,  height = 20, units = "cm")


gp_soe <- all_data %>% 
  dplyr::filter(measurement_type == "SOE", 
                Recording_Active_Electrode != Probe_Active_Electrode, 
                Recording_Active_Electrode != Probe_Indifferent_Electrode, 
                Recording_Active_Electrode != Masker_Active_Electrode, 
                Recording_Active_Electrode != Masker_Active_Electrode) %>%
  dplyr::group_by(probe_mode, Masker_Active_Electrode, rate) %>%
  ggplot(aes(Probe_Active_Electrode, 
             N1_P2_amp, 
             ymin=N1_P2_amp - amp_ci/2, 
             ymax=N1_P2_amp + amp_ci/2, 
             color=paste(rate), 
             group=paste(rate))) +
  geom_point() +
  geom_line() +
  geom_errorbar() +
  facet_grid(Masker_Active_Electrode ~ probe_mode) +
  ylab("Amplitude [uV]") +
  xlab("Probe electrode") +
  formater + 
  guides(color=guide_legend(title="Rate"))
gp_soe
ggsave(plot = gp_soe, paste(figures_path, "soe.png", sep=""),  width = 14,  height = 20, units = "cm")

