using BepInEx;
using BepInEx.IL2CPP;
using BepInEx.Configuration;
using HarmonyLib;
using Il2CppSystem.Collections.Generic;
using System;
using UnityEngine;
using UnhollowerBaseLib;
using UnhollowerRuntimeLib;
using UniverseLib;

// Made by Plasmatank. For Mystia's Izakaya.

namespace KokoroTest
{
    [BepInPlugin("Plasmatank.KokoroTest", "KokoroTest", "1.0.0")]
    public class Plugin : BasePlugin
    {
        public Harmony Harmony { get; } = new("VeryHarmonious");
        public ConfigEntry<string> ConfigName { get; private set; }

        public static BepInEx.Logging.ManualLogSource MyLogger;

        public static PlayerCore Kokoro;

        public static bool Get_Shield = false;

        public static Shield MyShield;


        public static void Print(object msg)
        {
            MyLogger.Log(BepInEx.Logging.LogLevel.Message, msg);
        }
        public override void Load()
        {
            MyLogger = Log;
            Log.LogInfo($"Plugin {PluginInfo.PLUGIN_GUID} is loaded!");
            Print("First Mod!");           
            Harmony.PatchAll();

            /*
            ClassInjector.RegisterTypeInIl2Cpp<RuntimeListener>();
            var Modifier = new GameObject("ModifierInstance");
            Modifier.AddComponent<RuntimeListener>();
            GameObject.DontDestroyOnLoad(Modifier);
            Modifier.hideFlags |= HideFlags.HideAndDontSave;
            */

        }
        [HarmonyPatch(typeof(PlayerCore), nameof(PlayerCore.Awake))]
        public static class AwakeHook
        {
            public static void Prefix(ref PlayerCore __instance)
            {
                Kokoro = __instance;
                Print("I'm awake!");
            }
        }

        [HarmonyPatch(typeof(PlayerCore), nameof(PlayerCore.AddShield))]
        public static class GetShieldHook
        {
            public static void Prefix(Shield shield)
            {
                Get_Shield = true;
                MyShield = shield;
                Print("I got a shield!");
            }
        }

        [HarmonyPatch(typeof(PlayerCore), nameof(PlayerCore.CostShield))]
        public static class ShieldHook
        {
            public static bool Prefix(ref PlayerCore __instance, ref float damage)
            {
                if (damage >= 5)
                {
                    damage *= 0.8f;
                }
                return true;
            }

            public static void Postfix(ref PlayerCore __instance)
            {                  
                Print("Cost: "+ Kokoro.aiShieldCostedNum.ToString());
            }
        }

        [HarmonyPatch(typeof(PlayerCore), nameof(PlayerCore.AttackEntity), new Type[] {typeof(EntityCore), typeof(EntityCore), typeof(DamageType), typeof(float)})]
        [HarmonyPatch(typeof(PlayerCore), nameof(PlayerCore.AttackEntity), new Type[] {typeof(EntityCore), typeof(EntityCore), typeof(AttackInfo), typeof(Il2CppSystem.Func<EntityCore, float, float>)})]
        public static class HitHook
        {
            public static bool Prefix(ref PlayerCore __instance, ref EntityCore target)
            {
                Print("Target hit!");              
                var EntityInstance = target.TryCast<EntityCore>();
                EntityInstance.BeHit(200f);
                if (__instance.aiShieldCostedNum > 0)
                {
                    Kokoro.CostShield(-(__instance.aiShieldCostedNum > 5 ? 5 : __instance.aiShieldCostedNum));
                    __instance.Heal(1f); 
                    __instance.BeHit(1f); //Refresh UI            
                }              
                return true;
            }
        }
        [HarmonyPatch(typeof(Mokou_SC1_Dash), nameof(Mokou_SC1_Dash.OnEnter))]
        public static class DashHook
        {
            public static void Postfix()
            {
                Print("Incoming!");
                var mokou = GameObject.FindObjectOfType<EntityCore>();
                mokou.BeHit(300f);
            }
        }

        [HarmonyPatch(typeof(EntityBuffList), nameof(EntityBuffList.InvincibleOn))]
        public static class TransHook
        {
            public static bool Prefix(ref EntityBuffList __instance)
            {
                Print("Invincible? Show off!");               
                return false;
            }
        }
    }

    public class RuntimeListener : MonoBehaviour
    {
        void Start()
        {
            Plugin.Print("Listener is loaded!");
        }

        void Update()
        {
            if(UniverseLib.Input.InputManager.GetKeyDown(KeyCode.Backspace))
            {
                Plugin.Print(Plugin.Kokoro.aiShieldCostedNum);
            }
        }
    }
}
