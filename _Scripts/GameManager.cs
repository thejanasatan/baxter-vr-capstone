using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : Singleton<GameManager> {
    protected GameManager() { } // guarantee this will be always a singleton only - can't use the constructor!

    public bool inCinematicMode;

    private void Awake()
    {
        
    }

    // (optional) allow runtime registration of global objects
    static public T RegisterComponent<T> () where T: Component
    {
        return Instance.GetOrAddComponent<T>();
    }
	//public bool isRunning;

	//// Use this for initialization
	//void Start () {
	//	isRunning = false;
	//}
	
	//// Update is called once per frame
	//void Update () {
		
	//}

	//public void EnableRunningState() {
	//	isRunning = true;
	//	return;
	//}
}