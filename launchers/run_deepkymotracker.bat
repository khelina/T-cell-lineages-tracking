@echo off
echo ========================================
echo        DeepKymoTracker Launcher
echo ========================================
echo.
echo Step 1 of 2: Trained Models Folder
echo This is where you placed the model files
echo downloaded from Zenodo.
echo Example: C:\Users\username\TRAINED_MODELS
echo.
set /p models_path="Trained models folder path: "

if not exist "%models_path%" (
    echo.
    echo ERROR: Folder not found: %models_path%
    echo Please check the path and try again.
    pause
    exit /b 1
)

echo.
echo Step 2 of 2: Movies Folder
echo This is where your cell movie files are stored.
echo Example: C:\Users\username\MOVIES
echo.
set /p movies_path="Movies folder path: "

if not exist "%movies_path%" (
    echo.
    echo ERROR: Folder not found: %movies_path%
    echo Please check the path and try again.
    pause
    exit /b 1
)

echo.
echo Starting DeepKymoTracker...
echo Note: Make sure VcXsrv is running before proceeding.
echo.

docker run -e DISPLAY=host.docker.internal:0 ^
           -v "%models_path%":/app/"TRAINED MODELS" ^
           -v "%movies_path%":/app/MOVIES ^
           khelinafedorchuk/deepkymotracker:latest

pause
