options(
 # repos=c(CRAN="https://cran.radicaldevelop.com/"),
 #repos=c(CRAN="https://cran.rstudio.com/"), 
 repos=c(CRAN="https://cloud.r-project.org/"),
  

  tidyverse.quiet = T
)

startup = function() {
  tryCatch({
    here::i_am("README.md")
    library(here)
    library(tidyverse)
    library(fastverse)
    library(conflicted)
    library(pak)
    conflicts_prefer(dplyr::filter)
    conflicts_prefer(lubridate::year)
  }, error = function(x) {
    MESSAGE_RSTUDIOAPIMISSING = "Some core packages are not installed, do installPackagesNeeded() to install them"
    MESSAGE_QUESTION = "Some core packages are probably not installed, do you want to install them now?"
    if (!require(rstudioapi) || !rstudioapi::isAvailable()) {
      warning(MESSAGE_RSTUDIOAPIMISSING)
      return(invisible())
    }
    rstudioapi::showQuestion("Packages", MESSAGE_QUESTION) -> answer
    if (answer) {
      installPackagesNeeded()
    }else {
      warning(MESSAGE_RSTUDIOAPIMISSING)
    }
  })
}


if (commandArgs()[[1]] == "RStudio") {
 setHook("rstudio.sessionInit", function(isNewSession) {
   startup()
 }, action = "append")
} else {
 startup()
}


# if (interactive() && getRversion() >= "4.0.0") {
#   globalCallingHandlers(
#     packageNotFoundError = function(err) {
#       MESSAGE = "Missing some package, wanna install all of them?"
#       rstudioapi::showQuestion("Packages", MESSAGE) -> answer
#       if (answer) {
#         installPackagesNeeded()
#         return(invisible())
#       }
#       NEXT_MESSAGE = "Do you want to try to install the missing one?"
#       rstudioapi::showQuestion("Packages", NEXT_MESSAGE) -> answer
#       if (answer) {
#         try(pak::handle_package_not_found(err))
#       }
#       stop(err)
#     }
#   )
# }

installPackagesNeeded <- function(reset = TRUE, ask = FALSE) {
  if (!require("devtools")) install.packages("devtools") # TODO change later 
  if (!require("pacman")) install.packages("pacman")
  pacman::p_unload("all")
  print("Reached here")
  # pak::local_install_dev_deps(ask = ask) # broken https://github.com/r-lib/pak/issues/567
  devtools::install_dev_deps()
  print("Reached here too")
  if (!reset) return()
  if (rstudioapi::isAvailable()) {
    rstudioapi::restartSession()
  } else {
    source(here::here(".Rprofile"))
  }
}

removeAllPacakges <- function() {
  pacman::p_unload("all")
  remove.packages(installed.packages( priority = "NA" )[,1] )
}

pkg_version <- function(pkg) {
  utils::packageVersion(pkg)
}

write_parquets <- function(archive_name, acidentes, condutores, passageiros, peoes, substitute = F) {
  library(here)
  # library(archive)
  write_ <- arrow::write_parquet
  
  
  # create dir if doesn't exit
  if (!dir.exists(here("data", archive_name))) {
    dir.create(here("data", archive_name))
  }
  
  write_(acidentes,   here("data", archive_name, "acidentes.parquet"))
  write_(condutores,  here("data", archive_name, "condutores.parquet"))
  write_(passageiros, here("data", archive_name, "passageiros.parquet"))
  write_(peoes,       here("data", archive_name, "peoes.parquet"))
  
  #create archive
  # por alguma razao isto corrempe os ficheiros
  # e rar n funciona~?
  # archive_write_dir(here("data", paste0(archive_name, ".zip")), here("data", archive_name), format = "zip")
  
  if (substitute) {
    warning("Substituting data in folder")
    lapply(c("acidentes", "condutores", "passageiros", "peoes"), \(x) {
      file.copy(
        here("data", archive_name, paste0(x, ".parquet")), 
        here("data", paste0(x, ".parquet")), 
        overwrite = T
      )
    })
  }
  # delete dir
  # unlink(here("data", archive_name), recursive = T)
}
