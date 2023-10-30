all:
	
test:
	pip install -qr requirements.txt
	cd pyeval && \
		DY_SIDECAR_PATH_INPUTS=test-inputs DY_SIDECAR_PATH_OUTPUTS=test-outputs \
		python main.py
	    
