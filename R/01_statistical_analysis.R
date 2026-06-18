library(tidyverse)
library(broom)

# Δημιουργία φακέλων εξόδου αν δεν υπάρχουν
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)

# Έλεγχος ότι υπάρχει το αρχείο δεδομένων
data_path <- "data/processed/recent_graduates_all_countries.csv"

if (!file.exists(data_path)) {
  stop("Δεν βρέθηκε το αρχείο: ", data_path)
}

# Φόρτωση δεδομένων
df <- read_csv(data_path, show_col_types = FALSE)

# Επιλογή τριτοβάθμιας εκπαίδευσης και Ελλάδας–ΕΕ
analysis_df <- df %>%
  filter(
    isced11 == "ED5-8",
    geo %in% c("EL", "EU27_2020")
  ) %>%
  mutate(
    time = as.numeric(time),
    value = as.numeric(value),
    country = if_else(geo == "EL", "Greece", "EU"),
    year_centered = time - min(time, na.rm = TRUE)
  ) %>%
  drop_na(time, value)

print(glimpse(analysis_df))

# Περιγραφικά στατιστικά
summary_table <- analysis_df %>%
  group_by(country) %>%
  summarise(
    observations = n(),
    mean_employment = mean(value),
    minimum = min(value),
    maximum = max(value),
    standard_deviation = sd(value),
    .groups = "drop"
  )

print(summary_table)

write_csv(
  summary_table,
  "outputs/tables/r_summary_statistics.csv"
)

# Γραμμικό μοντέλο
model <- lm(
  value ~ year_centered * country,
  data = analysis_df
)

print(summary(model))

model_results <- tidy(
  model,
  conf.int = TRUE
)

print(model_results)

write_csv(
  model_results,
  "outputs/tables/r_regression_results.csv"
)

# Γράφημα
trend_plot <- ggplot(
  analysis_df,
  aes(
    x = time,
    y = value,
    color = country
  )
) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 2.5) +
  geom_smooth(
    method = "lm",
    se = TRUE,
    linetype = "dashed"
  ) +
  scale_y_continuous(limits = c(40, 100)) +
  labs(
    title = "Employment of recent tertiary graduates",
    subtitle = "Comparison between Greece and the European Union",
    x = "Year",
    y = "Employment rate (%)",
    color = "Area",
    caption = "Source: Eurostat, dataset edat_lfse_24"
  ) +
  theme_minimal(base_size = 13)

print(trend_plot)

ggsave(
  "outputs/figures/r_employment_trend.png",
  trend_plot,
  width = 10,
  height = 6,
  dpi = 300
)

print("R analysis completed successfully.")