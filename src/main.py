import src.AppEngine as AppEngine

# Main of the whole AGV Simulator, calls loop declared deeper into Simulation
def main():
    app = AppEngine.AppEngine()
    app.LoopProgram()

if __name__ == "__main__":
    main()