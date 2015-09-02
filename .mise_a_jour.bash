#!/bin/bash

echo " -+-+- Veuillez attendre une dizaine de secondes que la mise a jour se fasse -+-+-"

cd ~/Code/pySpriteWorld
git fetch origin
git reset --hard origin/master

cd ~/Code/pyCommon
git fetch origin
git reset --hard origin/master

~/Code/pyCommon/.apres_maj
