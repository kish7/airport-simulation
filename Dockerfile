FROM conda/miniconda3
RUN conda create -n myenv python=3.6
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]
ENV PATH=/opt/conda/envs/env/bin:$PATH LC_ALL=C.UTF-8 LANG=C.UTF-8
RUN conda install -c conda-forge xorg-libx11 -y
RUN echo "source activate myenv" >> ~/.bashrc

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN mkdir -p ~/.config/matplotlib/ && echo "backend : Agg" >> ~/.config/matplotlib/matplotlibrc
RUN pip install -r requirements.txt
WORKDIR data/real-west-all-terminals
RUN python generate_scenario.py && python generate.py
WORKDIR ../../
CMD ["/bin/bash", "-c", "source activate myenv && flask run --host=0.0.0.0"]