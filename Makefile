# Makefile for source rpm: gawk
# $Id$
NAME := gawk
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
