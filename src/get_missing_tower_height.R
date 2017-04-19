#!/usr/bin/env Rscript

# Me borrowing Ned Haughton's web scrapping funcs from the fluxnetLSM package
# to grab the tower height information. This is super slow as the way I've
# implemented it you have to scrape the website for every site. Clearly that
# isn't the best way to do this. Should have another go later on.
# Also it would be good to catch errors due to missing height information.
#
# Note to self, might be an idea to just write this myself
#
# 19th April 2017

# Need to do this as I want to push the output back into python
suppressPackageStartupMessages(library(rvest))

#' Get a list of ORNL site URLs from site_status table
get_ornl_site_url_list <- function(site_code_list) {
    status_table_url <- "https://fluxnet.ornl.gov/site_status"
    page_html <- read_html(status_table_url)
    ornl_url_list <- list()

    for (site_code in site_code_list) {
        # looks for table cell with site code as contents, then looks up the parent
        # row, and finds the href of the first link.
        xpath <- paste0("//td[text()='", site_code, "']/..")
        trow <- tryCatch(page_html %>% html_node(xpath = xpath), error=function(e) NULL)
        if (class(trow) == "xml_node") {
            ornl_rel_url <- trow %>% html_node("a") %>% html_attr("href")
            ornl_url_list[[site_code]] <- paste0("https://fluxnet.ornl.gov/", ornl_rel_url)
        } else {
            message(site_code, " not found in table at https://fluxnet.ornl.gov/site_status")
        }
    }

    return(ornl_url_list)
}

get_site_ornl_url <- function(site_code) {
    ornl_url <- get_ornl_site_url_list(list(site_code))[[site_code]]
    return(ornl_url)
}

args <- commandArgs(TRUE)
site_code <- args[1]
#site_code = "US-Ha1"
site_url <- get_site_ornl_url(site_code)
page_html <- read_html(site_url)
table_data <- page_html %>% html_node("table#fluxnet_site_characteristics") %>% html_table()
tower_ht <- table_data[table_data[1] == "Tower Height:"][2]
tower_ht <- as.character(gsub("m", "", tower_ht))
cat(sprintf("%s\n", tower_ht))
